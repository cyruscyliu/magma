<?php
class TrampolineTest {
    public function __call(string $name, array $arguments) {
        var_dump($name, $arguments);
    }
}
$o = new TrampolineTest();
$callback = [$o, 'trampoline'];
$array = ["a" => "b", 1];
try {
    forward_static_call_array($callback, $array);
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
echo "Done\n";
?>