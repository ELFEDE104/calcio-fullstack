import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-dettaglio-squadra',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="container">
      <a routerLink="/squadre" class="back">← Torna alle squadre</a>
      <div *ngIf="loading">Caricamento...</div>
      <div *ngIf="!loading && errore">{{ errore }}</div>
      <div *ngIf="!loading && squadra">
        <h1>{{ squadra.nome_squadra }}</h1>
        <div class="sezione">
          <h2>📋 Informazioni</h2>
          <p>👤 Capitano: {{ squadra.capitano }}</p>
          <p>👔 Presidente: {{ squadra.presidente }}</p>
          <p>🏅 Ranking: {{ squadra.ranking }}</p>
          <p>🏆 Trofei: {{ squadra.trofei_vinti }}</p>
          <p>📅 Fondata: {{ squadra.anno_fondazione }}</p>
        </div>
        <div class="sezione" *ngIf="allenatore">
          <h2>🧑‍💼 Allenatore</h2>
          <p>{{ allenatore.nome }} {{ allenatore.cognome }}</p>
        </div>
        <div class="sezione" *ngIf="sponsor">
          <h2>💼 Sponsor</h2>
          <p>{{ sponsor.nome_sponsor }}</p>
        </div>
        <div class="sezione">
          <h2>⚽ Giocatori ({{ giocatori.length }})</h2>
          <div *ngFor="let g of giocatori" class="giocatore-card">
            <span class="maglia">#{{ g.num_maglia }}</span>
            <a [routerLink]="['/giocatori', g.id_giocatore]">{{ g.nome }} {{ g.cognome }}</a>
            <span class="ruolo">{{ g.ruolo }}</span>
          </div>
        </div>
      </div>
    </div>
  `
})
export class DettaglioSquadraComponent implements OnInit {
  squadra: any = null;
  allenatore: any = null;
  giocatori: any[] = [];
  sponsor: any = null;
  loading = true;
  errore = '';

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    const nome = this.route.snapshot.paramMap.get('nome');
    if (nome) {
      this.apiService.getDettaglioSquadra(nome).subscribe({
        next: (data: any) => {
          this.squadra = data.squadra;
          this.allenatore = data.allenatore;
          this.giocatori = data.giocatori;
          this.sponsor = data.sponsor;
          this.loading = false;
          this.cdr.detectChanges();
        },
        error: () => {
          this.errore = 'Squadra non trovata';
          this.loading = false;
          this.cdr.detectChanges();
        }
      });
    } else {
      this.loading = false;
      this.cdr.detectChanges();
    }
  }
}