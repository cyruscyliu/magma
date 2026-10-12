<?php

interface I {
    #[\Override]
    public function i(): void;
}

interface II extends I {}


class C implements II {
    public function i(): void {}
}

class C2 implements I {
    public function i(): void {}
}

echo "Done";

?>