import { Component, OnInit } from '@angular/core';
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
  loading: boolean = false;
  errore: string = '';

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loading = true;
    this.apiService.getClassifica().subscribe({
      next: (data) => {
        this.classifica = data;
        this.loading = false;
      },
      error: () => {
        this.errore = 'Errore nel caricamento della classifica';
        this.loading = false;
      }
    });
  }
}