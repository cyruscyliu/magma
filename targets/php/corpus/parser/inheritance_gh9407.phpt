<?php

class A {
    public function duplicate(): static {}
}

class C {
    public static function generate() {
        eval(<<<PHP
            class B extends A {
                public function duplicate(): A {}
            }
        PHP);
    }
}

C::generate();

?>