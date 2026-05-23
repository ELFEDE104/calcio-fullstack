import { Routes } from '@angular/router';
import { ListaSquadre } from './components/lista-squadre/lista-squadre';
import { DettaglioSquadra } from './components/dettaglio-squadra/dettaglio-squadra';
import { ListaGiocatori } from './components/lista-giocatori/lista-giocatori';
import { DettaglioGiocatore } from './components/dettaglio-giocatore/dettaglio-giocatore';
import { ListaPartite } from './components/lista-partite/lista-partite';
import { DettaglioPartita } from './components/dettaglio-partita/dettaglio-partita';
import { Classifica } from './components/classifica/classifica';

export const routes: Routes = [
  { path: '', redirectTo: '/squadre', pathMatch: 'full' },
  { path: 'squadre', component: ListaSquadre },
  { path: 'squadre/:nome', component: DettaglioSquadra },
  { path: 'giocatori', component: ListaGiocatori },
  { path: 'giocatori/:id', component: DettaglioGiocatore },
  { path: 'partite', component: ListaPartite },
  { path: 'partite/:id', component: DettaglioPartita },
  { path: 'classifica', component: Classifica },
  { path: '**', redirectTo: '/squadre' }
];