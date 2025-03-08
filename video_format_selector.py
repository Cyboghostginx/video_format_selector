import torch
import os
import folder_paths
import comfy.utils

class VideoFormatSelector:
    """
    Comprehensive custom node that generates latent video dimensions based on selected format preset.
    Includes landscape, portrait, square, and cinematic aspect ratios with multiple resolution options.
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
                ], {"default": "Landscape - 16:9 (720p)"}),
                "frames": ("INT", {"default": 33, "min": 1, "max": 240, "step": 1}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 4, "step": 1}),
                "custom_width": ("INT", {"default": 832, "min": 256, "max": 2048, "step": 8, "display": "custom"}),
                "custom_height": ("INT", {"default": 480, "min": 256, "max": 2048, "step": 8, "display": "custom"})
            }
        }
    
    RETURN_TYPES = ("LATENT",)
    FUNCTION = "get_format"
    CATEGORY = "Video Generation"
    
    def get_format(self, format, frames, batch_size, custom_width, custom_height):
        # Preset dimensions based on format selection
        presets = {
            "Landscape - 16:9 (480p)": (832, 480),
            "Landscape - 16:9 (720p)": (1280, 720),
            "Portrait - 9:16 (480p)": (480, 832),
            "Portrait - 9:16 (720p)": (720, 1280),
            "Square - 1:1 (512px)": (512, 512),
            "Square - 1:1 (768px)": (768, 768),
            "Custom Resolution": (custom_width, custom_height)
        }
        
        # Select dimensions from presets
        width, height = presets.get(format, (custom_width, custom_height))
        
        # Ensure dimensions are divisible by 8 (VAE requirement)
        width = width - (width % 8)
        height = height - (height % 8)
        
        # Create empty latent tensor with appropriate dimensions
        latent = torch.zeros([batch_size, 4, height // 8, width // 8])
        
        # Log selected format info
        print(f"Selected video format: {format}")
        print(f"Dimensions: {width}x{height}, Frames: {frames}, Batch size: {batch_size}")
        
        # Structure to match EmptyHunyuanLatentVideo format
        return ({"samples": latent, "frames": frames},)

# Node that provides video format information and recommendations
class VideoFormatInfo:
    """
    Provides information about different video formats and recommendations
    for specific platforms and use cases.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "platform": (
                    "General Dimension"
                ], {"default": "General Info"})
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "get_info"
    CATEGORY = "Video Generation"
    
    def get_info(self, platform):
        info = {
            "General Info": "Common video formats:\n- 16:9 (Landscape): Standard for most platforms\n- 9:16 (Portrait): Mobile optimized for stories/reels\n- 1:1 (Square): Universal compatibility\n- 4:5 (Portrait): Instagram feed optimal\n- 21:9 (Ultrawide): Cinematic look\n\nResolution terminology:\n- 480p: 832x480 (SD)\n- 720p: 1280x720 (HD)\n- 1080p: 1920x1080 (Full HD)\n- 1440p: 2560x1440 (QHD)\n- 2160p: 3840x2160 (4K UHD)"
        }
        
        return (info.get(platform, "Format information not available."),)

# Add nodes to ComfyUI
NODE_CLASS_MAPPINGS = {
    "VideoFormatSelector": VideoFormatSelector,
    "VideoFormatInfo": VideoFormatInfo
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoFormatSelector": "📽️ Video Format Selector",
    "VideoFormatInfo": "ℹ️ Video Format Info"
}
