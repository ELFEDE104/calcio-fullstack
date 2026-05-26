import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-classifica',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './classifica.html',
  styleUrl: './classifica.css'
})
export class ClassificaComponent implements OnInit {
  classifica: any[] = [];
  loading: boolean = true;
  errore: string = '';

  constructor(
    private apiService: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.apiService.getClassifica().subscribe({
      next: (data) => {
        this.classifica = data;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.errore = 'Errore nel caricamento della classifica';
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }
}