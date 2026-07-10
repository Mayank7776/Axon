import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

export interface ChatModel {
  id?: string;
  name: string;
  description: string;
  type: 'trainer' | 'nutrition' | 'workout designer';
}

@Component({
  selector: 'app-addchat',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './addchat.html',
  styleUrl: './addchat.css',
})
export class Addchat implements OnInit {
  @Input() existingModel: ChatModel | null = null;
  @Output() onSubmitModel = new EventEmitter<ChatModel>();
  @Output() onCancel = new EventEmitter<void>();

  modelForm: FormGroup;

  modelTypes = [
    { value: 'trainer', label: 'Trainer' },
    { value: 'nutrition', label: 'Nutritionist' },
    { value: 'workout designer', label: 'Workout Designer' }
  ];

  constructor(private fb: FormBuilder) {
    this.modelForm = this.fb.group({
      name: ['', Validators.required],
      description: ['', Validators.required],
      type: ['trainer', Validators.required]
    });
  }

  ngOnInit(): void {
    if (this.existingModel) {
      this.modelForm.patchValue(this.existingModel);
    }
  }

  onSubmit() {
    if (this.modelForm.valid) {
      const formValue = this.modelForm.value;
      this.onSubmitModel.emit({
        ...this.existingModel,
        ...formValue
      });
    }
  }

  cancel() {
    this.onCancel.emit();
  }
}
