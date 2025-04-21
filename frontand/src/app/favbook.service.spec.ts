import { TestBed } from '@angular/core/testing';
import {FavbookService} from "./favbook.service";


describe('FavbookService', () => {
  let service: FavbookService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FavbookService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
