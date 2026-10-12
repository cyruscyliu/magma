<?php

$x = new stdClass();

\var_dump(\clone($x));
\var_dump(\array_map('clone', [$x, $x, $x]));
\var_dump(\array_map(clone(...), [$x, $x, $x]));

class Foo {
    private function __clone() {
        
    }

    public function clone_me() {
        // Verify visibility when going through array_map().
        return array_map(\clone(...), [$this]);
    }
}

$f = new Foo();

$clone = $f->clone_me()[0];

var_dump($f !== $clone);

?>