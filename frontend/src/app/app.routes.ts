import { Routes } from '@angular/router';
import { ListaSquadreComponent } from './components/lista-squadre/lista-squadre';
import { DettaglioSquadraComponent } from './components/dettaglio-squadra/dettaglio-squadra';
import { ListaGiocatoriComponent } from './components/lista-giocatori/lista-giocatori';
import { DettaglioGiocatoreComponent } from './components/dettaglio-giocatore/dettaglio-giocatore';
import { ListaPartiteComponent } from './components/lista-partite/lista-partite';
import { DettaglioPartitaComponent } from './components/dettaglio-partita/dettaglio-partita';
import { ClassificaComponent } from './components/classifica/classifica';

export const routes: Routes = [
  { path: '', redirectTo: '/squadre', pathMatch: 'full' },
  { path: 'squadre', component: ListaSquadreComponent },
  { path: 'squadre/:nome', component: DettaglioSquadraComponent },
  { path: 'giocatori', component: ListaGiocatoriComponent },
  { path: 'giocatori/:id', component: DettaglioGiocatoreComponent },
  { path: 'partite', component: ListaPartiteComponent },
  { path: 'partite/:id', component: DettaglioPartitaComponent },
  { path: 'classifica', component: ClassificaComponent },
  { path: '**', redirectTo: '/squadre' }
];