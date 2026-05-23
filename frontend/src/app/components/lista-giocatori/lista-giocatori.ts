import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api';
import { Giocatore } from '../../models/giocatore.model';

@Component({
  selector: 'app-lista-giocatori',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  templateUrl: './lista-giocatori.html',
  styleUrl: './lista-giocatori.css'
})
export class ListaGiocatoriComponent implements OnInit {
  giocatori: Giocatore[] = [];
  filtroSquadra: string = '';
  filtroRuolo: string = '';
  loading: boolean = false;
  errore: string = '';

  ruoli = ['', 'Portiere', 'Difensore', 'Centrocampista', 'Attaccante'];

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.caricaGiocatori();
  }

  caricaGiocatori(): void {
    this.loading = true;
    this.errore = '';
    this.apiService.getGiocatori(this.filtroSquadra, this.filtroRuolo).subscribe({
      next: (data) => {
        this.giocatori = data;
        this.loading = false;
      },
      error: () => {
        this.errore = 'Errore nel caricamento dei giocatori';
        this.loading = false;
      }
    });
  }
}