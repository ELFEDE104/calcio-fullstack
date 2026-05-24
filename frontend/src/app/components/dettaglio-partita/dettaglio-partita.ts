import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-dettaglio-partita',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './dettaglio-partita.html',
  styleUrl: './dettaglio-partita.css'
})
export class DettaglioPartitaComponent implements OnInit {
  partita: any = null;
  eventi: any[] = [];
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
      this.apiService.getDettaglioPartita(id).subscribe({
        next: (data) => {
          this.partita = data.partita;
          this.eventi = data.eventi;
          this.infortuni = data.infortuni;
          this.loading = false;
        },
        error: () => {
          this.errore = 'Partita non trovata';
          this.loading = false;
        }
      });
    }
  }
}