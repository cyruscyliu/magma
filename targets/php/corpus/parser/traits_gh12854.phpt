<?php

trait SimpleTrait
{
    public function pub() {}
    protected function prot() {}
    private function priv() {}

    public final function final1() {}
    public final function final2() {}
    public final function final3() {}
}


class Test
{
    use SimpleTrait {
        pub as final;
        prot as final;
        priv as final;

        final1 as private;
        final2 as protected;
        final3 as public;
    }
}

foreach (['pub', 'prot', 'priv', 'final1', 'final2', 'final3'] as $method) {
    echo "--- Method: $method ---\n";
    $rm = new ReflectionMethod(Test::class, $method);
    var_dump($rm->isFinal());
    var_dump($rm->isPublic());
    var_dump($rm->isProtected());
    var_dump($rm->isPrivate());
}

?>