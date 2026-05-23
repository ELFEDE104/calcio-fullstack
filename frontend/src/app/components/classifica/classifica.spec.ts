import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Classifica } from './classifica';

describe('Classifica', () => {
  let component: Classifica;
  let fixture: ComponentFixture<Classifica>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Classifica],
    }).compileComponents();

    fixture = TestBed.createComponent(Classifica);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
