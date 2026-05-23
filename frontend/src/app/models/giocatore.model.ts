export interface Giocatore {
  id_giocatore: number;
  nome: string;
  cognome: string;
  eta: number;
  ruolo: string;
  squadra: string;
  nazionalita: string;
  num_maglia: number;
  stipendio?: number;
  clausola_rescissoria?: number;
  data_fine?: string;
}