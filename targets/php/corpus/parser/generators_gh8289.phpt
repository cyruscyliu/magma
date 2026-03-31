<?php

function yieldFromIteratorGeneratorThrows() {
	try {
		yield from new class(new ArrayIterator([1, -2])) extends IteratorIterator {
			public function key(): mixed {
				if ($k = parent::key()) {
					throw new Exception;
				}
				return $k;
			}
		};
	} catch (Exception $e) {
		echo "$e\n";
		yield 2;
	}
}

foreach (yieldFromIteratorGeneratorThrows() as $k => $v) {
    var_dump($v);
}

?>