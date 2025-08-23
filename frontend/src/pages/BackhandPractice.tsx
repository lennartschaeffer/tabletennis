import { useState } from "react";
import {
  Title,
  Text,
  Container,
  Stack,
  Button,
  Group,
  FileInput,
} from "@mantine/core";

const BackhandPractice = () => {
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
          Backhand Practice
        </Title>
        <Text ta="center" c="dimmed">
          Upload a video of your backhand practice session and receive
          AI-powered feedback on your technique.
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
              Analyze My Backhand
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
              <Text fw={500}>Backhand strokes detected:</Text>
              <Text>{results.backhand_count}</Text>
            </Group>
            <Group>
              <Text fw={500}>Quality score:</Text>
              <Text>{results.quality_score}/10</Text>
            </Group>
            <Group>
              <Text fw={500}>Consistency:</Text>
              <Text>{results.consistency}</Text>
            </Group>
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

export default BackhandPractice;
