// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract PetRegistry {
    struct Pet {
        string name;
        string kind;
        string breed;
        string color;
        uint256 age;
        string city;
        string pet_address;
        uint256 phone;
        string ownerName;
        string email;
    }

    mapping(uint256 => Pet) private pets;
    uint256 private petCount;

    function addPet(
        string memory _name,
        string memory _kind,
        string memory _breed,
        string memory _color,
        uint256 _age,
        string memory _city,
        string memory _pet_address,
        uint256 _phone,
        string memory _ownerName,
        string memory _email
    ) public {
        uint256 currentPetCount = petCount;
        pets[currentPetCount] = Pet(
            _name,
            _kind,
            _breed,
            _color,
            _age,
            _city,
            _pet_address,
            _phone,
            _ownerName,
            _email
        );
        petCount++;
    }

    function getPet(
        uint256 _petId
    )
        public
        view
        returns (
            string memory,
            string memory,
            string memory,
            string memory,
            uint256,
            string memory,
            string memory,
            uint256,
            string memory,
            string memory
        )
    {
        require(_petId < petCount, "Pet does not exist");
        Pet memory pet = pets[_petId];
        return (
            pet.name,
            pet.kind,
            pet.breed,
            pet.color,
            pet.age,
            pet.city,
            pet.pet_address,
            pet.phone,
            pet.ownerName,
            pet.email
        );
    }
}
