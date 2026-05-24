import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api';
import { Squadra } from '../../models/squadra.model';

@Component({
  selector: 'app-lista-squadre',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  templateUrl: './lista-squadre.html',
  styleUrl: './lista-squadre.css'
})
export class ListaSquadreComponent implements OnInit {
  squadre: Squadra[] = [];
  filtroNome: string = '';
  loading: boolean = false;
  errore: string = '';

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.caricaSquadre();
  }

  caricaSquadre(): void {
    this.loading = true;
    this.errore = '';
    this.apiService.getSquadre(this.filtroNome).subscribe({
      next: (data) => {
        this.squadre = data;
        this.loading = false;
      },
      error: (err) => {
        this.errore = 'Errore nel caricamento delle squadre';
        this.loading = false;
      }
    });
  }

  cercaSquadre(): void {
    this.caricaSquadre();
  }
}