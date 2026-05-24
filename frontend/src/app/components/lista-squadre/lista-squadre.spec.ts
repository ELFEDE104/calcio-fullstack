import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListaSquadre } from './lista-squadre';

describe('ListaSquadre', () => {
  let component: ListaSquadre;
  let fixture: ComponentFixture<ListaSquadre>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListaSquadre],
    }).compileComponents();

    fixture = TestBed.createComponent(ListaSquadre);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
