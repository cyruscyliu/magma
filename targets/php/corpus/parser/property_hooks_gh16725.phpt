<?php

class C implements JsonSerializable
{
    private string $prop1 { get => 'bar'; }

    public function __construct(
        private string $prop2,
    ) {}

    public function jsonSerialize(): mixed {
        return get_object_vars($this);
    }
}

$obj = new C('foo');
var_dump(get_object_vars($obj));
echo json_encode($obj);

?>