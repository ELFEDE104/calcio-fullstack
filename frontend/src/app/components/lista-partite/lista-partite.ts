import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api';
import { Partita } from '../../models/partita.model';

@Component({
  selector: 'app-lista-partite',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  templateUrl: './lista-partite.html',
  styleUrl: './lista-partite.css'
})
export class ListaPartiteComponent implements OnInit {
  partite: Partita[] = [];
  filtroSquadra: string = '';
  loading: boolean = false;
  errore: string = '';

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.caricaPartite();
  }

  caricaPartite(): void {
    this.loading = true;
    this.apiService.getPartite(this.filtroSquadra).subscribe({
      next: (data) => {
        this.partite = data;
        this.loading = false;
      },
      error: () => {
        this.errore = 'Errore nel caricamento delle partite';
        this.loading = false;
      }
    });
  }
}