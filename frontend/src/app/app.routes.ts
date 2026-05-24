import { Routes } from '@angular/router';
import { ListaSquadreComponent } from './components/lista-squadre/lista-squadre';
import { DettaglioSquadraComponent } from './components/dettaglio-squadra/dettaglio-squadra';
import { ListaGiocatoriComponent } from './components/lista-giocatori/lista-giocatori';
import { DettaglioGiocatoreComponent } from './components/dettaglio-giocatore/dettaglio-giocatore';
import { ListaPartiteComponent } from './components/lista-partite/lista-partite';
import { DettaglioPartitaComponent } from './components/dettaglio-partita/dettaglio-partita';
import { ClassificaComponent } from './components/classifica/classifica';
import { FormGiocatoreComponent } from './components/form-giocatore/form-giocatore';
import { FormSquadraComponent } from './components/form-quadra/form-quadra';
import { FormAllenatoreComponent } from './components/form-allenatore/form-allenatore';

export const routes: Routes = [
  { path: '', redirectTo: '/squadre', pathMatch: 'full' },
  { path: 'squadre', component: ListaSquadreComponent },
  { path: 'squadre/nuova', component: FormSquadraComponent },
  { path: 'squadre/:nome', component: DettaglioSquadraComponent },
  { path: 'squadre/:nome/modifica', component: FormSquadraComponent },
  { path: 'giocatori', component: ListaGiocatoriComponent },
  { path: 'giocatori/nuovo', component: FormGiocatoreComponent },
  { path: 'giocatori/:id', component: DettaglioGiocatoreComponent },
  { path: 'giocatori/:id/modifica', component: FormGiocatoreComponent },
  { path: 'partite', component: ListaPartiteComponent },
  { path: 'partite/:id', component: DettaglioPartitaComponent },
  { path: 'classifica', component: ClassificaComponent },
  { path: 'allenatori/nuovo', component: FormAllenatoreComponent },
  { path: 'allenatori/:id/modifica', component: FormAllenatoreComponent },
  { path: '**', redirectTo: '/squadre' }
];