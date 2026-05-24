import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DettaglioSquadra } from './dettaglio-squadra';

describe('DettaglioSquadra', () => {
  let component: DettaglioSquadra;
  let fixture: ComponentFixture<DettaglioSquadra>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DettaglioSquadra],
    }).compileComponents();

    fixture = TestBed.createComponent(DettaglioSquadra);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
