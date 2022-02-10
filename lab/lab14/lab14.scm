(define (split-at lst n)
  (cond 
    ((null? lst)
     (cons nil nil))
    ((= n 0)
     (cons nil lst))
    (else
     (cons (cons (car lst)
                 (car (split-at (cdr lst) (- n 1))))
           (cdr (split-at (cdr lst) (- n 1)))))))

(define (compose-all funcs)
  (define (helper pre funcs)
    (if (null? funcs)
        pre
        (helper (lambda (x) ((car funcs) (pre x)))
                (cdr funcs))))
  (helper (lambda (x) x) funcs))