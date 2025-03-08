import torch
import os
import folder_paths
import comfy.utils

class VideoFormatSelector:
    """
    Custom node for WAN video generation with preset formats and durations.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "format": ([
                    "Landscape - 16:9 (480p)",
                    "Landscape - 16:9 (720p)",
                    "Portrait - 9:16 (480p)",
                    "Portrait - 9:16 (720p)",
                    "Square - 1:1 (512px)",
                    "Square - 1:1 (768px)"
                ], {"default": "Landscape - 16:9 (480p)"}),
                "duration": ([
                    "Short (3 seconds / 72 frames)",
                    "Medium (5 seconds / 120 frames)",
                    "Long (8 seconds / 192 frames)",
                    "Custom frames"
                ], {"default": "Medium (5 seconds / 120 frames)"}),
                "custom_frames": ("INT", {"default": 33, "min": 1, "max": 240, "step": 1}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 4, "step": 1})
            }
        }
    
    RETURN_TYPES = ("LATENT",)
    FUNCTION = "get_format"
    CATEGORY = "latent"
    
    def get_format(self, format, duration, custom_frames, batch_size):
        # Preset dimensions based on format selection
        presets = {
            "Landscape - 16:9 (480p)": (832, 480),
            "Landscape - 16:9 (720p)": (1280, 720),
            "Portrait - 9:16 (480p)": (480, 832),
            "Portrait - 9:16 (720p)": (720, 1280),
            "Square - 1:1 (512px)": (512, 512),
            "Square - 1:1 (768px)": (768, 768)
        }
        
        # Duration presets (at 24fps)
        duration_frames = {
            "Short (3 seconds / 72 frames)": 72,
            "Medium (5 seconds / 120 frames)": 120,
            "Long (8 seconds / 192 frames)": 192,
            "Custom frames": custom_frames
        }
        
        # Select dimensions from presets
        width, height = presets.get(format, (832, 480))
        
        # Select frames based on duration
        frames = duration_frames.get(duration, custom_frames)
        
        # Ensure dimensions are divisible by 8 (VAE requirement)
        width = width - (width % 8)
        height = height - (height % 8)
        
        # Create empty latent tensor with appropriate dimensions
        latent = torch.zeros([batch_size, 4, height // 8, width // 8])
        
        seconds = frames / 24
        print(f"VideoFormatSelector: Creating {width}x{height} video with {frames} frames ({seconds:.2f} seconds at 24fps)")
        
        # Structure to match EmptyHunyuanLatentVideo format
        return ({"samples": latent, "frames": frames},)

# Direct drop-in replacement for EmptyHunyuanLatentVideo
class EmptyWANLatentVideo:
    """
    Direct replacement for EmptyHunyuanLatentVideo with identical interface.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"default": 832, "min": 256, "max": 2048, "step": 8}),
                "height": ("INT", {"default": 480, "min": 256, "max": 2048, "step": 8}),
                "frames": ("INT", {"default": 33, "min": 1, "max": 240, "step": 1}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 4, "step": 1})
            }
        }
    
    RETURN_TYPES = ("LATENT",)
    FUNCTION = "generate"
    CATEGORY = "latent"
    
    def generate(self, width, height, frames, batch_size):
        latent = torch.zeros([batch_size, 4, height // 8, width // 8])
        seconds = frames / 24
        print(f"EmptyWANLatentVideo: Creating {width}x{height} video with {frames} frames ({seconds:.2f} seconds at 24fps)")
        return ({"samples": latent, "frames": frames},)

# Add nodes to ComfyUI
NODE_CLASS_MAPPINGS = {
    "VideoFormatSelector": VideoFormatSelector,
    "EmptyWANLatentVideo": EmptyWANLatentVideo
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoFormatSelector": "📽️ Video Format & Duration Selector",
    "EmptyWANLatentVideo": "🎬 Empty WAN Video Latent"
}
