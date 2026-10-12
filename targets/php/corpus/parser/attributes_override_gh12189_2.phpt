<?php

class A {
    private function foo(): void {}
}

trait T {
    #[\Override]
    public function foo(): void {
        echo 'foo';
    }
}

class D extends A {
    use T;
}
echo "Done";

?>