import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormQuadra } from './form-quadra';

describe('FormQuadra', () => {
  let component: FormQuadra;
  let fixture: ComponentFixture<FormQuadra>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FormQuadra]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FormQuadra);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
