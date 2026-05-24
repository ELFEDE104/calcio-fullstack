import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-form-giocatore',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './form-giocatore.html',
  styleUrl: './form-giocatore.css'
})
export class FormGiocatoreComponent implements OnInit {

  modalita: 'inserimento' | 'modifica' = 'inserimento';
  id: number | null = null;
  loading: boolean = false;
  successo: string = '';
  errore: string = '';

  squadre: any[] = [];
  ruoli = ['Portiere', 'Difensore', 'Centrocampista', 'Attaccante'];

  giocatore = {
    id_giocatore: null,
    nome: '',
    cognome: '',
    eta: null,
    ruolo: '',
    squadra: '',
    nazionalita: '',
    num_maglia: null
  };

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: ApiService
  ) {}

  ngOnInit(): void {
    this.id = Number(this.route.snapshot.paramMap.get('id')) || null;
    this.modalita = this.id ? 'modifica' : 'inserimento';

    this.apiService.getSquadre().subscribe({
      next: (data) => this.squadre = data
    });

    if (this.modalita === 'modifica' && this.id) {
      this.loading = true;
      this.apiService.getDettaglioGiocatore(this.id).subscribe({
        next: (data) => {
          this.giocatore = { ...data.giocatore };
          this.loading = false;
        },
        error: () => {
          this.errore = 'Giocatore non trovato';
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
      this.apiService.inserisciGiocatore(this.giocatore).subscribe({
        next: () => {
          this.successo = 'Giocatore inserito con successo!';
          this.loading = false;
          setTimeout(() => this.router.navigate(['/giocatori']), 1500);
        },
        error: (err) => {
          this.errore = err.error?.errore || 'Errore durante il salvataggio';
          this.loading = false;
        }
      });
    } else {
      this.apiService.modificaGiocatore(this.id!, this.giocatore).subscribe({
        next: () => {
          this.successo = 'Giocatore modificato con successo!';
          this.loading = false;
          setTimeout(() => this.router.navigate(['/giocatori', this.id]), 1500);
        },
        error: (err) => {
          this.errore = err.error?.errore || 'Errore durante la modifica';
          this.loading = false;
        }
      });
    }
  }

  elimina(): void {
    if (!confirm('Sei sicuro di voler eliminare questo giocatore?')) return;
    this.loading = true;
    this.apiService.eliminaGiocatore(this.id!).subscribe({
      next: () => {
        this.successo = 'Giocatore eliminato!';
        this.loading = false;
        setTimeout(() => this.router.navigate(['/giocatori']), 1500);
      },
      error: (err) => {
        this.errore = err.error?.errore || 'Errore durante l\'eliminazione';
        this.loading = false;
      }
    });
  }
}