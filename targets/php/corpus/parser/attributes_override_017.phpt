<?php

trait T {
    public function t(): void {}
}

class C {
    use T;

    #[\Override]
    public function t(): void {}
}

echo "Done";

?>