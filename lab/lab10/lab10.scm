(define (over-or-under num1 num2)
  ;   (cond 
  ;     ((< num1 num2) -1)
  ;     ((= num1 num2) 0)
  ;     (else          1)))
  (if (< num1 num2)
      -1
      (if (= num1 num2)
          0
          1)))

(define (make-adder num) (lambda (x) (+ num x)))

(define (composed f g) (lambda (x) (f (g x))))

; (define lst (list (list 1) 2 (list 3 4) 5))
; (define lst (list '(1) 2 '(3 4) 5))
; (define lst '((1) 2 (3 4) 5))
(define lst
        (cons (cons 1 nil)
              (cons 2 (cons (cons 3 (cons 4 nil)) (cons 5 nil)))))

; (define (remove item lst)
;   (cond
;     ((null? lst)
;      lst)
;     ((= (car lst) item)
;      (remove item (cdr lst)))
;     (else
;      (cons (car lst) (remove item (cdr lst))))))
(define (remove item lst) (filter (lambda (i) (not (= i item))) lst))
