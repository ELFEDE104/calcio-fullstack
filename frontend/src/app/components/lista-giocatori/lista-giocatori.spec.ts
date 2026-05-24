import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListaGiocatori } from './lista-giocatori';

describe('ListaGiocatori', () => {
  let component: ListaGiocatori;
  let fixture: ComponentFixture<ListaGiocatori>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListaGiocatori],
    }).compileComponents();

    fixture = TestBed.createComponent(ListaGiocatori);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
