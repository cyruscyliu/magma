<?php

class C {
    public Closure $d = static function (E $e) {
        echo $e->secret, PHP_EOL;
    };

    
}

class E {
    public function __construct(
        private string $secret,
    ) {}
}

$c = new C();
($c->d)(new E('secret'));


?>