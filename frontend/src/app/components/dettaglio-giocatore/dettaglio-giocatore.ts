import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-dettaglio-giocatore',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dettaglio-giocatore.html',
  styleUrl: './dettaglio-giocatore.css'
})
export class DettaglioGiocatoreComponent implements OnInit {
  giocatore: any = null;
  contratto: any = null;
  infortuni: any[] = [];
  loading: boolean = false;
  errore: string = '';

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (id) {
      this.loading = true;
      this.apiService.getDettaglioGiocatore(id).subscribe({
        next: (data) => {
          this.giocatore = data.giocatore;
          this.contratto = data.contratto;
          this.infortuni = data.infortuni;
          this.loading = false;
        },
        error: () => {
          this.errore = 'Giocatore non trovato';
          this.loading = false;
        }
      });
    }
  }
}