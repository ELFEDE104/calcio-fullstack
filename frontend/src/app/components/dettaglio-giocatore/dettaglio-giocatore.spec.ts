import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DettaglioGiocatore } from './dettaglio-giocatore';

describe('DettaglioGiocatore', () => {
  let component: DettaglioGiocatore;
  let fixture: ComponentFixture<DettaglioGiocatore>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DettaglioGiocatore],
    }).compileComponents();

    fixture = TestBed.createComponent(DettaglioGiocatore);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
