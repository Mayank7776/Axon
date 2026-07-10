import { Component, OnInit, signal, ViewChild, ElementRef, inject, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { Chat as ChatService } from '../../services/chat';
import { User as UserService } from '../../services/user';

@Component({
  selector: 'app-chat',
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.html',
  styleUrl: './chat.css',
})
export class Chat implements OnInit, AfterViewChecked {
  private chatService = inject(ChatService);
  private userService = inject(UserService);
  private route = inject(ActivatedRoute);

  @ViewChild('messageContainer') private messageContainer!: ElementRef;

  // State Signals
  protected readonly users = signal<any[]>([]);
  protected readonly currentUserId = signal<string | null>(null);
  protected readonly sessions = signal<any[]>([]);
  protected readonly selectedSession = signal<any | null>(null);
  protected readonly messages = signal<any[]>([]);
  protected readonly selectedAgent = signal<string>('trainer'); // 'trainer', 'nutrition', 'designer'
  protected readonly newMessageText = signal<string>('');
  
  protected readonly isLoadingSessions = signal<boolean>(false);
  protected readonly isLoadingMessages = signal<boolean>(false);
  protected readonly isSending = signal<boolean>(false);
  
  // Controls if we show active chat panel on mobile
  protected readonly isChatActiveOnMobile = signal<boolean>(false);
  
  // New Chat Modal state
  protected readonly showNewChatModal = signal<boolean>(false);
  protected readonly newChatTitle = signal<string>('');

  // Track if we need to scroll to bottom
  private shouldScrollToBottom = false;

  ngOnInit() {
    this.loadUsersAndSessions();
    
    // Check for query parameters from Home Page routing
    this.route.queryParams.subscribe(params => {
      const agent = params['agent'];
      const isNewChat = params['newChat'];
      
      if (agent) {
        // Must wait slightly for user to be loaded if it's first render, 
        // but setting agent immediately is fine
        this.selectedAgent.set(agent);
        
        if (isNewChat === 'true') {
          // Open modal. If user isn't loaded yet, we can retry or just let the modal open
          setTimeout(() => this.openNewChatModal(), 300);
        }
      }
    });
  }

  ngAfterViewChecked() {
    if (this.shouldScrollToBottom) {
      this.scrollToBottom();
      this.shouldScrollToBottom = false;
    }
  }

  loadUsersAndSessions() {
    this.isLoadingSessions.set(true);
    // Fetch users list to select a default user in development mode
    this.userService.getUsers().subscribe({
      next: (response: any) => {
        const userList = response?.data || response;
        if (Array.isArray(userList) && userList.length > 0) {
          this.users.set(userList);
          // Default to first user found
          const defaultUserId = userList[0].id;
          this.currentUserId.set(defaultUserId);
          this.loadSessions(defaultUserId);
        } else {
          // Fallback to a seeded database user id if no users are returned
          const fallbackId = '633a23be-f628-49f5-8c4c-bb12b602532a';
          this.currentUserId.set(fallbackId);
          this.loadSessions(fallbackId);
        }
      },
      error: () => {
        // Fallback user ID in case of network or query failure
        const fallbackId = '633a23be-f628-49f5-8c4c-bb12b602532a';
        this.currentUserId.set(fallbackId);
        this.loadSessions(fallbackId);
      }
    });
  }

  loadSessions(userId: string, selectSessionId?: string) {
    this.isLoadingSessions.set(true);
    this.chatService.getSessions(userId).subscribe({
      next: (response: any) => {
        const sessionList = response?.data || response || [];
        this.sessions.set(sessionList);
        
        // Auto-select session if specified, or default to the most recent one
        if (selectSessionId) {
          const match = sessionList.find((s: any) => s.id === selectSessionId);
          if (match) this.selectSession(match);
        } else if (sessionList.length > 0) {
          // In desktop mode we can auto-select the first session.
          // In mobile, we keep it unselected so the user sees the list first.
          const isMobile = window.innerWidth < 768;
          if (!isMobile) {
            // Only select first session if we don't have a new chat modal open from query params
            if (!this.showNewChatModal()) {
              this.selectSession(sessionList[0]);
            }
          }
        } else {
          this.selectedSession.set(null);
          this.messages.set([]);
        }
        this.isLoadingSessions.set(false);
      },
      error: () => {
        this.isLoadingSessions.set(false);
      }
    });
  }

  selectSession(session: any) {
    this.selectedSession.set(session);
    this.selectedAgent.set(session.agent_type);
    this.isChatActiveOnMobile.set(true);
    this.loadMessages(session.id);
  }

  loadMessages(sessionId: string) {
    this.isLoadingMessages.set(true);
    this.chatService.getMessages(sessionId).subscribe({
      next: (response: any) => {
        const msgs = response?.data || response || [];
        this.messages.set(msgs);
        this.isLoadingMessages.set(false);
        this.shouldScrollToBottom = true;
      },
      error: () => {
        this.isLoadingMessages.set(false);
      }
    });
  }

  setAgent(agentType: string) {
    this.selectedAgent.set(agentType);
  }

  openNewChatModal() {
    const userId = this.currentUserId();
    if (!userId) return; // Note: if user isn't loaded yet, it might fail. setTimeout above handles this usually.
    this.newChatTitle.set('');
    this.showNewChatModal.set(true);
  }

  confirmNewChat() {
    const userId = this.currentUserId();
    if (!userId) return;

    let title = this.newChatTitle().trim();
    if (!title) {
      title = `${this.getAgentDisplayName(this.selectedAgent())} Consultation`;
    }

    const payload = {
      user_id: userId,
      agent_type: this.selectedAgent(),
      title: title
    };

    this.chatService.createSession(payload).subscribe({
      next: (response: any) => {
        const newSession = response?.data || response;
        if (newSession && newSession.id) {
          // Immediately prepend to local list and select
          this.sessions.update(list => [newSession, ...list]);
          this.selectSession(newSession);
        }
        this.showNewChatModal.set(false);
      },
      error: () => {
        this.showNewChatModal.set(false);
      }
    });
  }

  cancelNewChat() {
    this.showNewChatModal.set(false);
  }

  sendChatMessage() {
    const messageContent = this.newMessageText().trim();
    const session = this.selectedSession();
    if (!messageContent || !session || this.isSending()) return;

    // 1. Instantly append local user message in UI for ultra-responsiveness
    const localUserMessage = {
      id: 'local-' + Date.now(),
      role: 'user',
      content: messageContent,
      created_at: new Date().toISOString()
    };
    this.messages.update(msgs => [...msgs, localUserMessage]);
    this.newMessageText.set('');
    this.shouldScrollToBottom = true;
    
    // Set loading/sending state
    this.isSending.set(true);

    // 2. Transmit message to backend
    this.chatService.sendMessage({
      session_id: session.id,
      message: messageContent
    }).subscribe({
      next: (response: any) => {
        this.isSending.set(false);
        
        // Backend returns custom Response(success=True, message=..., data=...)
        if (response?.success && response.data) {
          const aiResponse = response.data;
          this.messages.update(msgs => [...msgs, {
            id: aiResponse.message_id,
            role: aiResponse.role,
            content: aiResponse.content,
            created_at: aiResponse.created_at
          }]);
        } else {
          // Display backend business-logic error message
          this.appendErrorMessage(response?.message || 'Server error occurred');
        }
        this.shouldScrollToBottom = true;
      },
      error: (err: any) => {
        this.isSending.set(false);
        const errorMessage = err?.error?.message || 'Failed to connect to AI agent.';
        this.appendErrorMessage(errorMessage);
        this.shouldScrollToBottom = true;
      }
    });
  }

  clearAllChatSessions() {
    if (!confirm('Are you sure you want to delete all chat sessions? This action cannot be undone.')) {
      return;
    }

    const userId = this.currentUserId();
    if (!userId || this.sessions().length === 0) return;

    // Delete sessions sequentially or clear list
    const deleteObservables = this.sessions().map(s => this.chatService.deleteSession(s.id));
    
    // We can clear locally first and delete them
    this.sessions.set([]);
    this.selectedSession.set(null);
    this.messages.set([]);
    this.isChatActiveOnMobile.set(false);

    // Call delete API for each session
    deleteObservables.forEach(obs => {
      obs.subscribe({
        error: (e: any) => console.error('Failed to delete session', e)
      });
    });
  }

  deleteSingleSession(event: Event, sessionId: string) {
    event.stopPropagation(); // Stop clicking card selection
    
    if (!confirm('Delete this chat session?')) return;

    this.chatService.deleteSession(sessionId).subscribe({
      next: () => {
        const isCurrentSelected = this.selectedSession()?.id === sessionId;
        
        // Remove from sessions list
        this.sessions.update(list => list.filter(s => s.id !== sessionId));
        
        if (isCurrentSelected) {
          this.selectedSession.set(null);
          this.messages.set([]);
          this.isChatActiveOnMobile.set(false);
          
          // Try to select another if we have any left (desktop only)
          const list = this.sessions();
          if (list.length > 0 && window.innerWidth >= 768) {
            this.selectSession(list[0]);
          }
        }
      }
    });
  }

  goBackToSessionsList() {
    this.isChatActiveOnMobile.set(false);
    this.selectedSession.set(null);
  }

  private appendErrorMessage(text: string) {
    this.messages.update(msgs => [...msgs, {
      id: 'error-' + Date.now(),
      role: 'system_error',
      content: `⚠️ Error: ${text}`,
      created_at: new Date().toISOString()
    }]);
  }

  private scrollToBottom(): void {
    try {
      this.messageContainer.nativeElement.scrollTop = this.messageContainer.nativeElement.scrollHeight;
    } catch (err) {
      // Container not fully loaded yet
    }
  }

  // Helpers to check agent details for headers and lists
  getAgentIconUrl(agentType: string): string {
    switch (agentType) {
      case 'trainer': return '/Images/home/PersonalTrainner.png';
      case 'nutrition': return '/Images/home/Nutrition.png';
      case 'designer': return '/Images/home/WorkoutDesigner.png';
      default: return '/Images/home/PersonalTrainner.png';
    }
  }

  getAgentDisplayName(agentType: string): string {
    switch (agentType) {
      case 'trainer': return 'AI Personal Trainer';
      case 'nutrition': return 'AI Nutritionist';
      case 'designer': return 'AI Workout Designer';
      default: return 'AI Coach';
    }
  }

  getAgentThemeClass(agentType: string): string {
    switch (agentType) {
      case 'trainer': return 'bg-violet-600';
      case 'nutrition': return 'bg-emerald-600';
      case 'designer': return 'bg-orange-500';
      default: return 'bg-violet-600';
    }
  }

  getAgentBgLight(agentType: string): string {
    switch (agentType) {
      case 'trainer': return 'bg-violet-100/70 border-violet-200';
      case 'nutrition': return 'bg-emerald-100/70 border-emerald-200';
      case 'designer': return 'bg-orange-100/70 border-orange-200';
      default: return 'bg-violet-100/70 border-violet-200';
    }
  }

  // AI Response Parsing Helpers
  isWorkoutPlan(content: string): boolean {
    if (!content) return false;
    // Check if it has the key structure of a workout plan JSON
    return content.includes('"day_number"') && content.includes('"exercises"');
  }

  extractWorkoutPlan(content: string): any {
    try {
      // Try to find JSON inside markdown fences first (```json ... ``` or ``` ... ```)
      const match = content.match(/```(?:json)?\s*([\s\S]*?)```/);
      let jsonString = '';
      
      if (match && match[1]) {
        jsonString = match[1];
      } else {
        // If no markdown fences, try to extract from first { to last }
        const startIndex = content.indexOf('{');
        const endIndex = content.lastIndexOf('}');
        if (startIndex !== -1 && endIndex !== -1 && endIndex > startIndex) {
            jsonString = content.substring(startIndex, endIndex + 1);
        } else {
            return null; // Not valid json object structure
        }
      }
      
      return JSON.parse(jsonString);
    } catch (e) {
      console.error("Failed to parse workout plan JSON", e);
      return null;
    }
  }
  
  extractTextBeforePlan(content: string): string {
    if (!content) return '';
    // Extract text before markdown fence
    const fenceIndex = content.indexOf('```');
    if (fenceIndex !== -1) {
        return content.substring(0, fenceIndex).trim();
    }
    // Or text before the first opening brace
    const braceIndex = content.indexOf('{');
    if (braceIndex !== -1) {
        return content.substring(0, braceIndex).trim();
    }
    return content;
  }
}
