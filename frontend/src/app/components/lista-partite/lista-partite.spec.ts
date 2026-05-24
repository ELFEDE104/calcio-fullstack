import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListaPartite } from './lista-partite';

describe('ListaPartite', () => {
  let component: ListaPartite;
  let fixture: ComponentFixture<ListaPartite>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListaPartite],
    }).compileComponents();

    fixture = TestBed.createComponent(ListaPartite);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
