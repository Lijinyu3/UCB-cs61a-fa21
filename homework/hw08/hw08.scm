(define (my-filter func lst)
  (if (null? lst)
      nil
      (if (func (car lst))
          (cons (car lst) (my-filter func (cdr lst)))
          (my-filter func (cdr lst)))))

(define (interleave s1 s2)
  (cond 
    ((and (null? s1) (null? s2))
     nil)
    ((not (null? s1))
     (cons (car s1) (interleave s2 (cdr s1))))
    (else
     (interleave s2 s1))))

(define (accumulate merger start n term)
  (if (= n 0)
      start
      (merger (term n)
              (accumulate merger start (- n 1) term))))

(define (no-repeats lst)
  (if (null? lst)
      lst
      (cons (car lst)
            (no-repeats
             (my-filter (lambda (x) (not (= x (car lst))))
                        (cdr lst))))))
