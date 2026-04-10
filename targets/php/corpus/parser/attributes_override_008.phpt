<?php

trait T {
    #[\Override]
    public function t(): void {}
}

class Foo {
    use T;
}

echo "Done";

?>