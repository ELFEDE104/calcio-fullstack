import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
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
  loading: boolean = true;
  errore: string = '';

  constructor(
    private route: ActivatedRoute,
    private apiService: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (id) {
      this.apiService.getDettaglioPartita(id).subscribe({
        next: (data) => {
          this.partita = data.partita;
          this.eventi = data.eventi;
          this.infortuni = data.infortuni;
          this.loading = false;
          this.cdr.detectChanges();
        },
        error: () => {
          this.errore = 'Partita non trovata';
          this.loading = false;
          this.cdr.detectChanges();
        }
      });
    } else {
      this.loading = false;
    }
  }
}