<?php

trait T {
    public abstract function t(): void;
}

class C {
    use T;

    #[\Override]
    public function t(): void {}
}

echo "Done";

?>