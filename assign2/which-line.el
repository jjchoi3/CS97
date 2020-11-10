(defun which-line ()
  "Print the current buffer line number and narrowed line number of point."
  (interactive)
  (let ((start (point-min))
	(n (line-number-at-pos))
	(lines (count-lines (point-min) (point-max))))
    (if (= (point-max) 1)
	(setq lastChar 1)
      (setq lastChar (char-before (point-max))))
      (if (/= lastChar 10)
	   (message "Line %d of %d" n (- lines 1))
      (if (= start 1)
	  (message "Line %d of %d" n lines)
	 (save-excursion
	   (save-restriction
	     (widen)
	     (message "line %d (narrowed line %d)"
		      (+ n (line-number-at-pos start) -1) n)))))))
