from dataclasses import dataclass, asdict

@dataclass(slots=True)
class GeminiModel:
    
    name: str
    display_name: str
    description: str
    version: str
    input_token_limit: int
    output_token_limit: int
    supported_actions: list[str]

    @classmethod
    def from_api(cls, model):
        
        return cls(
            name=model.name,
            display_name=model.display_name,
            description=getattr(model, 'description', 'No description'),
            version=getattr(model, 'version', 'Unknown'),
            input_token_limit=getattr(model, 'input_token_limit', 0),
            output_token_limit=getattr(model, 'output_token_limit', 0), 
            supported_actions=getattr(model, 'supported_actions', [])
        )

    def to_dict(self):
        return asdict(self)
