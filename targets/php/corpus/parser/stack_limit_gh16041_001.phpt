<?php

class Canary {
    public function __destruct() {
        new Canary();
    }
}

new Canary();

?>