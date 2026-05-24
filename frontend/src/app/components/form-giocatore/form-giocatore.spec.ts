import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormGiocatoreComponent } from './form-giocatore';

describe('FormGiocatoreComponent', () => {
  let component: FormGiocatoreComponent;
  let fixture: ComponentFixture<FormGiocatoreComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FormGiocatoreComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FormGiocatoreComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
