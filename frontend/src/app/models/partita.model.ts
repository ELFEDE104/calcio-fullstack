export interface Partita {
  id_partita: number;
  meteo: string;
  orario_partita: string;
  squadra: string;
  squadra_ospite: string;
  arbitro: string;
  data_partita: string;
  id_competizione: number;
  giornata: number;
  risultato: number;
  nome_stadio: string;
  competizione?: string;
}