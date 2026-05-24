import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Squadra } from '../models/squadra.model';
import { Giocatore } from '../models/giocatore.model';
import { Partita } from '../models/partita.model';
import { Allenatore } from '../models/allenatore.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  // =============================================
  // SQUADRE
  // =============================================

  getSquadre(nome?: string): Observable<Squadra[]> {
    let params = new HttpParams();
    if (nome) params = params.set('nome', nome);
    return this.http.get<Squadra[]>(`${this.apiUrl}/squadre`, { params });
  }

  getDettaglioSquadra(nomeSquadra: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/squadre/${nomeSquadra}`);
  }

  // =============================================
  // GIOCATORI
  // =============================================

  getGiocatori(squadra?: string, ruolo?: string, nazionalita?: string): Observable<Giocatore[]> {
    let params = new HttpParams();
    if (squadra) params = params.set('squadra', squadra);
    if (ruolo) params = params.set('ruolo', ruolo);
    if (nazionalita) params = params.set('nazionalita', nazionalita);
    return this.http.get<Giocatore[]>(`${this.apiUrl}/giocatori`, { params });
  }

  getDettaglioGiocatore(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/giocatori/${id}`);
  }

  // =============================================
  // PARTITE
  // =============================================

  getPartite(squadra?: string): Observable<Partita[]> {
    let params = new HttpParams();
    if (squadra) params = params.set('squadra', squadra);
    return this.http.get<Partita[]>(`${this.apiUrl}/partite`, { params });
  }

  getDettaglioPartita(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/partite/${id}`);
  }

  // =============================================
  // CLASSIFICA E ALLENATORI
  // =============================================

  getClassifica(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/classifica`);
  }

  getAllenatori(): Observable<Allenatore[]> {
    return this.http.get<Allenatore[]>(`${this.apiUrl}/allenatori`);
  }
}