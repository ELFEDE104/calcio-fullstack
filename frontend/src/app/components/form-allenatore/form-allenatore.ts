import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-form-allenatore',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './form-allenatore.html',
  styleUrl: './form-allenatore.css'
})
export class FormAllenatoreComponent implements OnInit {

  modalita: 'inserimento' | 'modifica' = 'inserimento';
  id: number | null = null;
  loading: boolean = false;
  successo: string = '';
  errore: string = '';
  squadre: any[] = [];

  allenatore: any = {
    nome: '',
    cognome: '',
    eta: 0,
    nazionalita: '',
    squadra: '',
    trofei_vinti: 0
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
      this.apiService.getAllenatori().subscribe({
        next: (data) => {
          const found = data.find((a: any) => a.id_allenatore === this.id);
          if (found) {
            this.allenatore = { ...found };
          } else {
            this.errore = 'Allenatore non trovato';
          }
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
      this.apiService.inserisciAllenatore(this.allenatore).subscribe({
        next: () => {
          this.successo = 'Allenatore inserito con successo!';
          this.loading = false;
          setTimeout(() => this.router.navigate(['/squadre']), 1500);
        },
        error: (err) => {
          this.errore = err.error?.errore || 'Errore durante il salvataggio';
          this.loading = false;
        }
      });
    } else {
      this.apiService.modificaAllenatore(this.id!, this.allenatore).subscribe({
        next: () => {
          this.successo = 'Allenatore modificato con successo!';
          this.loading = false;
          setTimeout(() => this.router.navigate(['/squadre']), 1500);
        },
        error: (err) => {
          this.errore = err.error?.errore || 'Errore durante la modifica';
          this.loading = false;
        }
      });
    }
  }

  elimina(): void {
    if (!confirm('Sei sicuro di voler eliminare questo allenatore?')) return;
    this.loading = true;
    this.apiService.eliminaAllenatore(this.id!).subscribe({
      next: () => {
        this.successo = 'Allenatore eliminato!';
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