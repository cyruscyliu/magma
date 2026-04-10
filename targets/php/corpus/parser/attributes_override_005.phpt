<?php

interface I {
    public function i(): void;
}

class C extends P implements I {}

class P {
    #[\Override]
    public function i(): void {}
}

echo "Done";

?>