# Skill: Create Datatable

This skill details how to implement server-side paginated, searchable, and sortable tables in the Angular frontend.

## Guidelines

1. **State Management**:
   Use standard Angular Signals to maintain grid configuration state:
   ```typescript
   protected readonly filter = signal<DataTableFilter>({
     page: 1,
     limit: 10,
     search: '',
     sort_by: 'created_at',
     sort_order: 'desc'
   });
   ```
2. **Column Sorting**:
   Implement sort toggle headers that update `sort_by` and `sort_order` then trigger list reload:
   ```typescript
   toggleSort(column: string) {
     const current = this.filter();
     const nextOrder = (current.sort_by === column && current.sort_order === 'asc') ? 'desc' : 'asc';
     this.filter.set({
       ...current,
       sort_by: column,
       sort_order: nextOrder
     });
     this.loadData();
   }
   ```
3. **Query Search Debouncing**:
   When binding search input keywords, debounce event emissions using RxJS to avoid overload requests to the backend:
   ```typescript
   // In component ngOnInit or stream construction
   this.searchSubject.pipe(
     debounceTime(400),
     distinctUntilChanged(),
     takeUntilDestroyed()
   ).subscribe(query => {
     this.filter.update(f => ({ ...f, search: query, page: 1 }));
     this.loadData();
   });
   ```

## HTML UI Sample

```html
<div class="overflow-x-auto bg-slate-900 rounded-lg shadow p-4">
  <!-- Search Bar -->
  <input type="text" placeholder="Search..." (input)="onSearch($event)" 
         class="mb-4 p-2 bg-slate-800 border border-slate-700 text-white rounded w-64 focus:outline-none" />

  <!-- Data Grid -->
  <table class="w-full text-left text-sm text-slate-300">
    <thead class="bg-slate-850 text-white uppercase text-xs">
      <tr>
        <th class="p-3 cursor-pointer select-none" (click)="toggleSort('name')">
          Name <span *ngIf="filter().sort_by === 'name'">{{ filter().sort_order === 'asc' ? '▲' : '▼' }}</span>
        </th>
        <th class="p-3">Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr *ngFor="let item of items()" class="border-b border-slate-800 hover:bg-slate-800">
        <td class="p-3">{{ item.name }}</td>
        <td class="p-3">
          <button (click)="onDelete(item.id)" class="text-red-500 hover:underline">Delete</button>
        </td>
      </tr>
    </tbody>
  </table>

  <!-- Pagination Controls -->
  <div class="flex justify-between items-center mt-4 text-xs">
    <span>Page {{ filter().page }}</span>
    <div class="flex gap-2">
      <button [disabled]="filter().page === 1" (click)="changePage(-1)" 
              class="p-2 bg-slate-850 rounded hover:bg-slate-800 disabled:opacity-50">Previous</button>
      <button [disabled]="isLastPage()" (click)="changePage(1)" 
              class="p-2 bg-slate-850 rounded hover:bg-slate-800 disabled:opacity-50">Next</button>
    </div>
  </div>
</div>
```
