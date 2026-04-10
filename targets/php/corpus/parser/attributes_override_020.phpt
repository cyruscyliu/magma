<?php

interface I {
    public function i(): void;
}

new class () implements I {
    public function i(): void {}

    #[\Override]
    public function c(): void {}
};

echo "Done";

?>