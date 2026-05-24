import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-form-squadra',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './form-quadra.html',
  styleUrl: './form-quadra.css'
})
export class FormSquadraComponent implements OnInit {

  modalita: 'inserimento' | 'modifica' = 'inserimento';
  nomeOriginale: string = '';
  loading: boolean = false;
  successo: string = '';
  errore: string = '';

  squadra = {
    nome_squadra: '',
    capitano: '',
    ranking: null,
    presidente: '',
    anno_fondazione: null,
    num_giocatori: 25,
    trofei_vinti: 0
  };

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: ApiService
  ) {}

  ngOnInit(): void {
    const nome = this.route.snapshot.paramMap.get('nome');
    const url = this.route.snapshot.url.join('/');

    if (nome && url.includes('modifica')) {
      this.modalita = 'modifica';
      this.nomeOriginale = nome;
      this.loading = true;
      this.apiService.getDettaglioSquadra(nome).subscribe({
        next: (data) => {
          this.squadra = { ...data.squadra };
          this.loading = false;
        },
        error: () => {
          this.errore = 'Squadra non trovata';
          this.loading = false;
        }
      });
    }
  }

  salva(): void {
    this.loading = true;
    this.errore = '';
    this.successo = '';

    if (this.modalita === 'inserimento') {
      this.apiService.inserisciSquadra(this.squadra).subscribe({
        next: () => {
          this.successo = 'Squadra inserita con successo!';
          this.loading = false;
          setTimeout(() => this.router.navigate(['/squadre']), 1500);
        },
        error: (err) => {
          this.errore = err.error?.errore || 'Errore durante il salvataggio';
          this.loading = false;
        }
      });
    } else {
      this.apiService.modificaSquadra(this.nomeOriginale, this.squadra).subscribe({
        next: () => {
          this.successo = 'Squadra modificata con successo!';
          this.loading = false;
          setTimeout(() => this.router.navigate(['/squadre', this.nomeOriginale]), 1500);
        },
        error: (err) => {
          this.errore = err.error?.errore || 'Errore durante la modifica';
          this.loading = false;
        }
      });
    }
  }

  elimina(): void {
    if (!confirm('Sei sicuro di voler eliminare questa squadra?')) return;
    this.loading = true;
    this.apiService.eliminaSquadra(this.nomeOriginale).subscribe({
      next: () => {
        this.successo = 'Squadra eliminata!';
        this.loading = false;
        setTimeout(() => this.router.navigate(['/squadre']), 1500);
      },
      error: (err) => {
        this.errore = err.error?.errore || 'Errore durante l\'eliminazione';
        this.loading = false;
      }
    });
  }
}