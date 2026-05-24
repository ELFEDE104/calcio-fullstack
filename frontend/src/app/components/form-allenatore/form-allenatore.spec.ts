import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormAllenatore } from './form-allenatore';

describe('FormAllenatore', () => {
  let component: FormAllenatore;
  let fixture: ComponentFixture<FormAllenatore>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FormAllenatore]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FormAllenatore);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
