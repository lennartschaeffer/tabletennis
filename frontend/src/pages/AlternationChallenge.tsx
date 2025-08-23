import { useState } from "react";
import {
  Title,
  Text,
  Container,
  Stack,
  Button,
  Group,
  FileInput,
  Progress,
} from "@mantine/core";

const AlternationChallenge = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [results, setResults] = useState<any>(null);

  const handleSubmit = async () => {
    if (!file) return;

    setUploading(true);

    try {
    } catch (error) {
      console.error("Error uploading video:", error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <Container size="md" py="xl">
      <Stack gap="lg">
        <Title order={2} ta="center">
          Alternation Challenge
        </Title>
        <Text ta="center" c="dimmed">
          Upload a video of your practice session where you alternate between
          forehand and backhand strokes. Our AI will analyze how well you switch
          between techniques.
        </Text>

        {!results ? (
          <>
            <FileInput
              label="Upload your practice video"
              placeholder="Click to select a video file"
              accept="video/*"
              value={file}
              onChange={setFile}
              size="md"
            />

            <Button
              onClick={handleSubmit}
              disabled={!file || uploading}
              loading={uploading}
              fullWidth
            >
              Analyze My Alternation
            </Button>
          </>
        ) : (
          <Stack
            gap="md"
            p="md"
            style={{ border: "1px solid #eaeaea", borderRadius: "8px" }}
          >
            <Title order={3}>Analysis Results</Title>
            <Group>
              <Text fw={500}>Forehand strokes:</Text>
              <Text>{results.forehand_count}</Text>
            </Group>
            <Group>
              <Text fw={500}>Backhand strokes:</Text>
              <Text>{results.backhand_count}</Text>
            </Group>
            <Stack gap="xs">
              <Text fw={500}>Alternation score:</Text>
              <Progress value={results.alternation_score} color="blue" />
              <Text size="sm" ta="center">
                {results.alternation_score}%
              </Text>
            </Stack>
            <Stack gap="xs">
              <Text fw={500}>Sequences detected:</Text>
            </Stack>
            <Group>
              <Text fw={500}>Feedback:</Text>
              <Text>{results.feedback}</Text>
            </Group>
            <Button onClick={() => setResults(null)} variant="outline">
              Upload Another Video
            </Button>
          </Stack>
        )}
      </Stack>
    </Container>
  );
};

export default AlternationChallenge;
