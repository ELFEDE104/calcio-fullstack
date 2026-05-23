import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-dettaglio-squadra',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dettaglio-squadra.html',
  styleUrl: './dettaglio-squadra.css'
})
export class DettaglioSquadraComponent implements OnInit {
  squadra: any = null;
  allenatore: any = null;
  giocatori: any[] = [];
  sponsor: any = null;
  loading: boolean = false;
  errore: string = '';

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService
  ) {}

  ngOnInit(): void {
    const nome = this.route.snapshot.paramMap.get('nome');
    if (nome) {
      this.loading = true;
      this.apiService.getDettaglioSquadra(nome).subscribe({
        next: (data) => {
          this.squadra = data.squadra;
          this.allenatore = data.allenatore;
          this.giocatori = data.giocatori;
          this.sponsor = data.sponsor;
          this.loading = false;
        },
        error: () => {
          this.errore = 'Squadra non trovata';
          this.loading = false;
        }
      });
    }
  }
}